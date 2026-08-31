from pathlib import Path
import shutil
import tarfile
import subprocess
import os
import pandas as pd
import random
import splitfolders


def setup_spam_corpus(raw_data_dir: Path, force_download: bool = False):
    """
    Downloads, extracts, and flattens the SpamAssassin public corpus.
    Skips downloading if the data already exists, unless force_download=True.
    """
    raw_data_dir = Path(raw_data_dir)
    corpus_dir = raw_data_dir / "spam_assassin_corpus"

    if raw_data_dir.exists() and not force_download:
        print(f"Data already exists in {raw_data_dir}. Skipping download.")
        return raw_data_dir

    if raw_data_dir.exists():
        shutil.rmtree(raw_data_dir)
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading SpamAssassin corpus archives...")
    wget_cmd = [
        "wget", "-r", "-q", "-np", "-nd",
        "-P", str(corpus_dir),
        "-A", "*.bz2,readme.html",
        "-X", "/old/publiccorpus/obsolete/",
        "https://spamassassin.apache.org/old/publiccorpus/"
    ]
    subprocess.run(wget_cmd, check=True)

    # 2. Extract tar.bz2 archives
    print("Extracting archives...")
    for archive in corpus_dir.glob("*.tar.bz2"):
        # Extracts to a folder named without the '.tar.bz2' suffix
        folder_name = archive.name.replace(".tar.bz2", "")
        extract_path = raw_data_dir / folder_name
        
        with tarfile.open(archive, "r:bz2") as tar:
            tar.extractall(extract_path)

    # 3. Flatten nested subdirectories created during extraction
    print("Flattening extracted folders...")
    for parent_dir in raw_data_dir.iterdir():
        if not parent_dir.is_dir() or parent_dir == corpus_dir:
            continue

        for child_dir in [d for d in parent_dir.iterdir() if d.is_dir()]:
            for file in child_dir.iterdir():
                if file.name != "cmds":
                    # Overwrite target if exists to avoid conflicts
                    dest = parent_dir / file.name
                    if dest.exists():
                        dest.unlink()
                    shutil.move(str(file), str(parent_dir))
            
            shutil.rmtree(child_dir)

    # 4. Relocate readme.html and clean up raw archive folder
    readme_src = corpus_dir / "readme.html"
    if readme_src.exists():
        shutil.move(str(readme_src), str(raw_data_dir / "readme.html"))

    if corpus_dir.exists():
        shutil.rmtree(corpus_dir)

    print("Dataset setup complete.")
    return raw_data_dir


def inspect_file(folder_name, file_type, raw_data_dir: Path):
    """
    Displays the content of a sample file from the specified folder.
    """
    sample_filename = os.listdir(raw_data_dir / folder_name)[0]
    sample_file = raw_data_dir / folder_name / sample_filename
    with open(sample_file, 'r', encoding='latin-1') as f:
        text = f.read()
    print(f"Sample {file_type}: {sample_filename}\n")
    print(text)


def detect_duplicates(raw_data_dir: Path, remove_duplicates: bool = False):
    """
    Detects duplicate emails in the raw data directory.
    If remove_duplicates is True, it will delete the duplicate files.
    Returns a set of duplicate emails and the count of duplicates found.
    """
    seen_emails = set()
    duplicate_emails = set()
    number_of_duplicates = 0

    for parent_dir in raw_data_dir.iterdir():
        if not parent_dir.is_dir():
            continue

        for file in parent_dir.iterdir():
            with open(file, 'r', encoding='latin-1') as f:
                text = f.read()
                if text in seen_emails:
                    number_of_duplicates += 1
                    duplicate_emails.add(text)
                    if remove_duplicates:
                        os.remove(file)
                else:
                    seen_emails.add(text)

    print(f"Total number of duplicates: {number_of_duplicates}")
    
    return duplicate_emails, number_of_duplicates


def get_data_info(raw_data_dir: Path) -> pd.DataFrame:
    """
    Get information about the data in the raw data directory.
    """

    def count_files_w_o_duplicates(folder, duplicate_files) -> int:
        if duplicate_files is None:
            return len(os.listdir(raw_data_dir / folder))
        
        res = len(os.listdir(raw_data_dir / folder))
        for f in os.listdir(raw_data_dir / folder):
            with open(raw_data_dir / folder / f, 'r', encoding='latin-1') as file:
                text = file.read()
                if text in duplicate_files:
                    res -= 1
                else:
                    duplicate_files.add(text)

        return res

    duplicate_files = set()

    data_info = pd.DataFrame(columns=['folder', 'type'])
    data_info['folder'] = os.listdir(raw_data_dir)
    data_info.drop(data_info[data_info['folder'] == 'readme.html'].index, inplace=True)
    data_info['type'] = data_info['folder'].apply(lambda x: 'spam' if 'spam' in x else 'ham')

    data_info['files_count_w_duplicates'] = data_info['folder'].apply(lambda x: len(os.listdir(raw_data_dir / x)))
    data_info['files_count_w/o_duplicates'] = data_info['folder'].apply(lambda x: count_files_w_o_duplicates(x, duplicate_files))

    total_files_w_duplicates = data_info['files_count_w_duplicates'].sum()
    total_spam_files_w_duplicates = data_info[data_info['type'] == 'spam']['files_count_w_duplicates'].sum()
    total_ham_files_w_duplicates = data_info[data_info['type'] == 'ham']['files_count_w_duplicates'].sum()

    total_files_w_o_duplicates = data_info['files_count_w/o_duplicates'].sum()
    total_spam_files_w_o_duplicates = data_info[data_info['type'] == 'spam']['files_count_w/o_duplicates'].sum()
    total_ham_files_w_o_duplicates = data_info[data_info['type'] == 'ham']['files_count_w/o_duplicates'].sum()

    pct_spam_w_duplicates = total_spam_files_w_duplicates / total_files_w_duplicates * 100
    print(f"Total files: {total_files_w_duplicates}")
    print(f"Total spam files: {total_spam_files_w_duplicates}")
    print(f"Total ham files: {total_ham_files_w_duplicates}")
    print(f"Percentage of spam: {pct_spam_w_duplicates:.2f}%")

    pct_spam_w_o_duplicates = total_spam_files_w_o_duplicates / total_files_w_o_duplicates * 100
    print("\nAfter removing duplicates:")
    print(f"Total files (w/o duplicates): {total_files_w_o_duplicates}")
    print(f"Total spam files (w/o duplicates): {total_spam_files_w_o_duplicates}")
    print(f"Total ham files (w/o duplicates): {total_ham_files_w_o_duplicates}")
    print(f"Percentage of spam: {pct_spam_w_o_duplicates:.2f}%")

    msc_info = {
        "total_files_w_duplicates": total_files_w_duplicates,
        "total_spam_files_w_duplicates": total_spam_files_w_duplicates,
        "total_ham_files_w_duplicates": total_ham_files_w_duplicates,

        "total_files_w_o_duplicates": total_files_w_o_duplicates,
        "total_spam_files_w_o_duplicates": total_spam_files_w_o_duplicates,
        "total_ham_files_w_o_duplicates": total_ham_files_w_o_duplicates,

        "pct_spam_w_duplicates": pct_spam_w_duplicates,
        "pct_spam_w_o_duplicates": pct_spam_w_o_duplicates,

        "duplicate_emails": total_files_w_duplicates - total_files_w_o_duplicates
    }
    return data_info, msc_info


def create_train_test_split(
    raw_data_dir, data_split_dir, seed=42, 
    train_ratio=0.8, test_ratio=0.2):

    # create train/test split on folders
    if os.path.exists(f'{data_split_dir}'):
        shutil.rmtree(f'{data_split_dir}')
    splitfolders.ratio(f'{raw_data_dir}', output=f'{data_split_dir}', 
            seed=seed, ratio=(train_ratio, 0.0, test_ratio), group_prefix=None, shuffle=True)

    # collect file paths for train and test
    def collect_file_paths(file_type):
        res = []
        for folder in Path(data_split_dir / file_type).iterdir():
            if folder.is_dir():
                res.extend([f for f in Path(folder).iterdir() if f.is_file()])
        return res

    train_files = collect_file_paths('train')
    test_files = collect_file_paths('test')

    # collect train or test file contents and labels
    def collect_file_contents(file_list, shuffle=True):
        X = []
        y = []
    
        if shuffle:
            random.seed(seed)
            random.shuffle(file_list)

        for f in file_list:
            with open(f, 'r', encoding='latin-1') as file:
                text = file.read()
            X.append(text)
            y.append(1 if 'spam' in str(f) else 0)
        return X, y

    X_train, y_train = collect_file_contents(train_files)
    X_test, y_test = collect_file_contents(test_files)

    return X_train, y_train, X_test, y_test