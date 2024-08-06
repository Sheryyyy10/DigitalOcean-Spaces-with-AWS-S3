# DigitalOcean-Spaces-with-AWS-S3
DigitalOcean Spaces is an object storage service that is compatible with the AWS S3 API, making it easy to use S3-compatible libraries and tools. 

# Django API with DigitalOcean Spaces

This project provides a Django API for performing CRUD (Create, Read, Update, Delete) operations on files stored in DigitalOcean Spaces, which is compatible with AWS S3. The API uses the `boto3` library to interact with DigitalOcean Spaces.

## Features

- **Create**: Upload new files to DigitalOcean Spaces.
- **Read**: Retrieve file details and download files from DigitalOcean Spaces.
- **Update**: Replace existing files in DigitalOcean Spaces.
- **Delete**: Remove files from DigitalOcean Spaces.

## Requirements

- Python 3.x
- Django
- `boto3` (for interacting with DigitalOcean Spaces)
- `django-storages` (for integration with Django)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/django-digitalocean-spaces.git
    cd django-digitalocean-spaces
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure DigitalOcean Spaces settings in Django:**

    Add the following to your `settings.py`:

    ```python
    # settings.py
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = 'your-access-key-id'
    AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_REGION_NAME = 'your-region-name'  # e.g., 'nyc3'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.nyc3.digitaloceanspaces.com'
    ```

5. **Migrate the database:**

    ```bash
    python manage.py migrate
    ```

6. **Run the Django development server:**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

- **Create File**
    - **URL:** `/api/files/`
    - **Method:** `POST`
    - **Description:** Upload a new file to DigitalOcean Spaces.
    - **Data:** `multipart/form-data` with file

- **Read File**
    - **URL:** `/api/files/<file_id>/`
    - **Method:** `GET`
    - **Description:** Retrieve file details and download the file.
    
- **Update File**
    - **URL:** `/api/files/<file_id>/`
    - **Method:** `PUT`
    - **Description:** Replace an existing file.
    - **Data:** `multipart/form-data` with file

- **Delete File**
    - **URL:** `/api/files/<file_id>/`
    - **Method:** `DELETE`
    - **Description:** Remove a file from DigitalOcean Spaces.

## Usage

You can test the API endpoints using tools like Postman or cURL. Ensure you have valid credentials and the bucket exists in DigitalOcean Spaces.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or fixes
