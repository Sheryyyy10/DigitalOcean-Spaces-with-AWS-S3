from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class SpacesView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            session = boto3.session.Session()
            client = session.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            response = client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            files = [{'Key': obj['Key'], 'Size': obj['Size']} for obj in response.get('Contents', [])]

            return Response({'files': files}, status=status.HTTP_200_OK)

        except NoCredentialsError:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
        except PartialCredentialsError:
            return Response({'error': 'Incomplete credentials provided'}, status=status.HTTP_403_FORBIDDEN)
        except client.exceptions.NoSuchBucket:
            return Response({'error': 'The specified bucket does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
            # Get the list of uploaded files
            files = request.FILES.getlist('file')
            if not files:
                return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
            app_name = request.data.get('app_name', '').strip()

            uploaded_files = []
            try:
                session = boto3.session.Session()
                client = session.client(
                    's3',
                    region_name=settings.AWS_S3_REGION_NAME,
                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )

                # Iterate over each file and upload it
                for file_obj in files:
                    # Define the file path in the bucket, including the folder
                    if app_name:
                        file_path = f"{app_name}/{file_obj.name}"
                    else:
                        file_path = f"{file_obj.name}"

                    # Upload the file to S3
                    client.upload_fileobj(
                        file_obj,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        file_path,
                        ExtraArgs={'ACL': 'public-read'}
                    )

                    file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}"
                    uploaded_files.append({
                        'file_name': file_obj.name,
                        'url': file_url
                    })

                return Response({'message': 'Files uploaded successfully', 'files': uploaded_files},
                                status=status.HTTP_201_CREATED)

            except NoCredentialsError:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
            except PartialCredentialsError:
                return Response({'error': 'Incomplete credentials provided'}, status=status.HTTP_403_FORBIDDEN)
            except client.exceptions.NoSuchBucket:
                return Response({'error': 'The specified bucket does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
            file_obj = request.FILES.get('file')
            if not file_obj:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

            file_name = request.data.get('file_name')
            if not file_name:
                return Response({'error': 'File name not specified'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                session = boto3.session.Session()
                client = session.client(
                    's3',
                    region_name=settings.AWS_S3_REGION_NAME,
                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )

                # Define the file path in the bucket, including the folder
                file_path = f"funswap/{file_name}"

                # Upload the new file to replace the existing one
                client.upload_fileobj(
                    file_obj,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    file_path,
                    ExtraArgs={'ACL': 'public-read'}
                )

                file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}"
                return Response({'message': 'File updated successfully', 'url': file_url}, status=status.HTTP_200_OK)

            except NoCredentialsError:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
            except PartialCredentialsError:
                return Response({'error': 'Incomplete credentials provided'}, status=status.HTTP_403_FORBIDDEN)
            except client.exceptions.NoSuchBucket:
                return Response({'error': 'The specified bucket does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        file_name = request.query_params.get('file_name')
        if not file_name:
            return Response({'error': 'File name not specified'}, status=status.HTTP_400_BAD_REQUEST)

        app_name = request.data.get('app_name', '').strip()

        try:
            session = boto3.session.Session()
            client = session.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            # Define the file path in the bucket, including the folder
            if app_name:
                file_path = f"{app_name}/{file_name}"
            else:
                file_path = f"{file_name}"

            # Delete the file from the bucket
            client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path
            )

            return Response({'message': 'File deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except NoCredentialsError:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
        except PartialCredentialsError:
            return Response({'error': 'Incomplete credentials provided'}, status=status.HTTP_403_FORBIDDEN)
        except client.exceptions.NoSuchBucket:
            return Response({'error': 'The specified bucket does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except client.exceptions.NoSuchKey:
            return Response({'error': 'The specified file does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateFolderView(APIView):
    def post(self, request, *args, **kwargs):
        folder_name = request.data.get('folder_name')
        if not folder_name:
            return Response({'error': 'No folder name provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = boto3.session.Session()
            client = session.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            # Define the folder path in the bucket (ends with a slash)
            folder_path = f"{folder_name}/"

            # Create a zero-byte object with the folder name
            client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=folder_path
            )

            folder_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{folder_path}"
            return Response({'message': 'Folder created successfully', 'url': folder_url}, status=status.HTTP_201_CREATED)

        except NoCredentialsError:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
        except PartialCredentialsError:
            return Response({'error': 'Incomplete credentials provided'}, status=status.HTTP_403_FORBIDDEN)
        except client.exceptions.BucketAlreadyExists:
            return Response({'error': 'The specified bucket already exists'}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
