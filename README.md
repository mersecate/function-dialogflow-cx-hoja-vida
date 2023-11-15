# Function: generate_pdf

## Description:

This Python Cloud Function is designed to generate a PDF document based on input data provided via a JSON request. The generated PDF includes information such as personal details, educational background, work experience, and a professional profile. The function performs additional tasks, including uploading the generated PDF to a Cloud Storage bucket, sending an email with the PDF attachment, and updating relevant information in a MySQL database.

## Dependencies:

Ensure that the following dependencies are installed before deploying the function:

- google-cloud-storage
- google-cloud-firestore
- google-cloud-functions
- xhtml2pdf
- mysql-connector
- asyncio

You can install these dependencies using the following pip command:

```bash
pip install google-cloud-storage google-cloud-firestore google-cloud-functions xhtml2pdf mysql-connector-python asyncio
```

Make sure to have the necessary credentials and access rights set up for Cloud Storage, Firestore, Cloud Functions, and MySQL.

## Environment Variables:

The function relies on the following environment variables:

- `secretos`: A JSON-formatted string containing various secrets required for authentication and configuration. Ensure this variable is set with the necessary values.

## Usage:

1. Deploy the function to your Google Cloud environment.
2. Set the required environment variables.
3. Trigger the function by sending a JSON request with the necessary data, such as personal information, educational details, work experience, etc.

```json
{
  "sessionInfo": {
    "session": "your_session_info_here",
    "parameters": {
      "nombre": "John Doe",
      "cargo": "Software Engineer",
      "email": "john.doe@example.com",
      "telefono": "123-456-7890",
      "nivelestudiomasalto": "Master's Degree",
      "nivelestudiomasalto_titulo": "Computer Science",
      "nivelestudiomasalto_institucion": "University of Example",
      "nivelestudiomasalto_formacion": {
        "day": 1,
        "month": 1,
        "year": 2020
      },
      "experiencialaboral": "Yes",
      "experiencialaboral_empresa": "Tech Solutions Inc.",
      "experiencialaboral_puesto": "Senior Software Engineer",
      "experiencialaboral_fecha": {
        "day": 1,
        "month": 1,
        "year": 2018
      },
      "experiencialaboral_actualidad": "No",
      "experiencialaboral_cese": {
        "day": 1,
        "month": 1,
        "year": 2022
      },
      "experiencialaboral_funciones": "Leading software development projects",
      "experiencialaboral_logros": "Successfully delivered multiple projects on time and within budget",
      "perfil_professional": "Results-driven software engineer with expertise in..."
    }
  }
}
```

4. The function will generate a PDF, upload it to the specified Cloud Storage bucket, and send an email with the PDF attachment. It will also update relevant information in the MySQL database.

Note: Adjust the JSON request according to your data structure and requirements.
