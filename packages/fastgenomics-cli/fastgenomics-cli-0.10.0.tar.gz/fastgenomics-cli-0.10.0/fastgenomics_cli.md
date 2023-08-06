# FASTGenomics CLI

This package is a collection of scripts to manage your data on [FASTGenomics](https://beta.fastgenomics.org).

It can be installed via

```bash
pip install fastgenomics-cli
```
and contains the following tools

## FASTGenomics Upload

This script is used to upload files via the command line.

### Usage

```bash
fg-upload [-h] [-v] [-d DATASET] [-u USER] [-p PASSWORD] [-t TITLE] [-m] file [file ...]

positional arguments:
  file                  the file(s) to be uploaded

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         more verbose output (default: False)
  -d DATASET, --dataset DATASET
                        add file to existing dataset with this id (default: None)
  -u USER, --user USER  your username (or email address) (default: None)
  -p PASSWORD, --password PASSWORD
                        your password (default: None)
  -t TITLE, --title TITLE
                        the title of the new dataset (default: None)
  -m, --metadata        upload files as metadata instead of expression data (default: False)
```

## FASTGenomics CLI

This script is a generic command line interface for FASTGenomics.

### Usage

```bash
fg-cli -h 
```


output
```bash
usage: fg-cli [-h] {login,logout,configure-aws,version,lfs,dataset} ...

 ______       _____ _______ _____                            _
|  ____/\    / ____|__   __/ ____|                          (_)
| |__ /  \  | (___    | | | |  __  ___ _ __   ___  _ __ ___  _  ___ ___
|  __/ /\ \  \___ \   | | | | |_ |/ _ \ '_ \ / _ \| '_ ` _ \| |/ __/ __|
| | / ____ \ ____) |  | | | |__| |  __/ | | | (_) | | | | | | | (__\__ \
|_|/_/    \_\_____/   |_|  \_____|\___|_| |_|\___/|_| |_| |_|_|\___|___/

Welcome to FASTGenomics CLI!

Here are the base commands:

optional arguments:
  -h, --help            show this help message and exit

FASTGenomics CLI:
  {login,logout,configure-aws,version,lfs,dataset}
                        Actions for FASTGenomics
    login               Log in to FASTGenomics.
    logout              Log out to remove access to FASTGenomics.
    configure-aws       Configure AWS for FASTGenomics
    version             Show the version of FASTGenomics CLI.
    lfs                 Manage Large File Storage (lfs)
    dataset             Manage datasets
```

### common
#### login

```bash
fg-cli login -h
```


output
```bash
usage: fg-cli login [-h] [-v] -u USER -p PASSPHRASE [-m {pat,password}]
                   [--url URL]

Log in to FASTGenomics.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -u USER, --user USER  the FASTGenomics user
  -p PASSPHRASE, --passphrase PASSPHRASE
                        the passphrase of FASTGenomics user
  -m {pat,password}, --login_method {pat,password}
                        the login method 'pat' (personal access token) or 'password'. Default: pat
  --url URL             the url of the FASTGenomics plattform. Default: https://beta.fastgenomics.org
```

#### logout

```bash
fg-cli logout -h
```


output
```bash
usage: fg-cli logout [-h] [-v]

Log out to remove access to FASTGenomics.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

#### version

```bash
fg-cli version -h
```


output
```bash
usage: fg-cli version [-h] [-v]

Show the version of the cli client

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

### dataset

```bash
fg-cli dataset -h
```


output
```bash
usage: fg-cli dataset [-h] {upload-file,delete} ...

Group: fg dataset - Manage FASTGenomics datasets.

positional arguments:
  {upload-file,delete}
    upload-file         upload files to FASTGenomics dataset
    delete              delete a FASTGenomics dataset

optional arguments:
  -h, --help            show this help message and exit
```

#### upload file to dataset

```bash
fg-cli dataset upload-file
```


output
```bash
usage: fg-cli dataset upload-file [-h] [-v] -id ID
                                 [-t [{expressiondata,metadata}]]
                                 files [files ...]

upload files to FASTGenomics dataset

positional arguments:
  files                 file names of the files to be uploaded

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -id ID                the id of the dataset
  -t [{expressiondata,metadata}], --type [{expressiondata,metadata}]
                        the type of the file 'expressionData' or 'metaData': Default: expressionData
```

#### delete dataset

```bash
fg-cli dataset delete
```


output
```bash
usage: fg-cli dataset delete [-h] [-v] -id ID

delete a FASTGenomics dataset

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
  -id ID         the id of the dataset
```

### large file storage (lfs)

```bash
fg-cli lfs -h
```


output
```bash
usage: fg-cli lfs [-h] [-v] {create,get-url} ...

Group: fg lfs  - Manage FASTGenomics Large File Storage (lfs)

positional arguments:
  {create,get-url}
    create          Create and upload a large file storage
    get-url         Get a download url

optional arguments:
  -h, --help        show this help message and exit
  -v, --verbose     Activate verbose output
```

#### create lfs

```bash
fg-cli lfs create
```


output
```bash
usage: fg-cli lfs create [-h] [-v] [-z [ZIP_FILENAME]] [-P [ZIP_PASSWORD]] -r
                        RECIPIENT_EMAIL [-T [TITLE]]
                        [--provider [{azure,aws}]] [--skip-compression]
                        files_or_directory [files_or_directory ...]

Create and upload a large file storage

positional arguments:
  files_or_directory    file names or directory to be compressed

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -z [ZIP_FILENAME], --zip-filename [ZIP_FILENAME]
                        name of the zip file
  -P [ZIP_PASSWORD], --zip-password [ZIP_PASSWORD]
                        password for the zip file. if omitted a password will be generated.
  -r RECIPIENT_EMAIL, --recipient-email RECIPIENT_EMAIL
                        the email address used in FASTGenomics of the recipient
  -T [TITLE], --title [TITLE]
                        the title of the FASTGenomics dataset containing the uploaded data
  --provider [{azure,aws}]
                        the provider to be used 'azure' or 'aws'. Default: azure)
  --skip-compression    Skip the compression
```

#### get url of lfs

```bash
fg-cli lfs get-url
```


output
```bash
usage: fg-cli lfs get-url [-h] [-v] id access_token

Get a download url

positional arguments:
  id             the id of the storage
  access_token   the access token

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

#### configure AWS

```bash
fg-cli configure-aws -h
```


output
```bash
usage: fg-cli configure-aws [-h] [-v]

Configure AWS for FASTGenomics

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```