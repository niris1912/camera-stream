# Project for Camera Streaming

## Clone this repository into your local

```sh
git clone https://github.com/niris1912/camera-stream.git
```

This repository consists of 2 parts
- camera-backend: Django Streaming Server
- camera-frontend: React Frontend Server


## Backend
You need to install python 3.8 or later.
And then install packages for backend project, and run backend server.

Run shell on root directory of this repository.
```sh
cd camera-backend
pip install -r requirements.txt
python manage.py runserver
```

## Frontend
You need to install nodejs v18 or later.
And then install packages for frontend project, and run frontend server.

Run shell on root directory of this repository.
```sh
cd camera-backend
npm install
npm run dev
```

if you use yarn for package manager

```sh
cd camera-backend
yarn install
yarn dev
```

## Testing
I used `vite` package to create react project, and run, so default port is 5173. <br>
Open your web browser, then go to the http://localhost:5173