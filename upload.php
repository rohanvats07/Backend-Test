<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        .upload-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }

        .file-upload {
            margin-top: 20px;
        }

        .file-upload input {
            display: none;
        }

        .file-upload label {
            background-color: #3498db;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            display: inline-block;
        }
    </style>
</head>
<body>

<div class="upload-container">
    <h2>Welcome to the Upload Page</h2>
    
    <div class="file-upload">
        <input type="file" id="fileInput" accept=".pptx, .docx, .xlsx" style="display:none" onchange="validateFileType()">
        <label for="fileInput">Upload File</label>
    </div>
</div>

<script>
    function validateFileType() {
        const fileInput = document.getElementById('fileInput');
        const allowedTypes = ['pptx', 'docx', 'xlsx'];
        const fileName = fileInput.value.toLowerCase();
        const fileType = fileName.split('.').pop();

        if (allowedTypes.includes(fileType)) {
            alert('File uploaded successfully!');
        } else {
            alert('Invalid file type. Please upload pptx, docx, or xlsx files.');
            fileInput.value = ''; // Clear the file input
        }
    }
</script>

</body>
</html>
