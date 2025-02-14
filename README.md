# StudyOnBlockchainApps

# Dataset
Primary dataset is collected from Das et al : https://github.com/disa-lab/BlockchainEmpiricalEASE2022. Follow these steps to download the dataset:

1. Enable Git Large File Storage

```
For Windows:
- Download git-lfs from the official site (download) and install it in your machine.
- Then set up Git LFS for your user account by running the following command in your terminal: `git lfs install`

For Mac:
brew install git-lfs
git lfs install

For Ubuntu:
sudo apt install git-lfs
git lfs install
```
2. Clone: `git clone https://github.com/disa-lab/BlockchainEmpiricalEASE2022.git`

# Prerequisites
1. Python 3.8
2. Install packages from `requirements.txt`
3. Create a `config` file in the root directory and place your github access token in it
```
{
    "access_token": "access token"
}
```