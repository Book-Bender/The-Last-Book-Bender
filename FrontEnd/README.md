# CSE6242 Demo App Frontend

This app uses Vite+React+MaterialUI component library.

For the backend, we will be using Flask. You can look at the current state of this frontend on the vercel link.

## Developing Locally

To start locally, there are several things needed to be done.

Firstly, we need to get the dependencies working. Inside the top level of this directory named `frontend`, do:

```bash
pip3 install -r requirements.txt
npm install
```

These two steps first installs the required packages for the python backend, then installs the needed javascript libraries. Optionally, you can start a python virtual environment before installing the python things.

To run the live server, there are two options.

1. In your terminal, execute `python3 app.py` to start flask.
2. After this step you can choose to either:
    * Option 1: Follow the link given by the command you just ran in the terminal to the browser (it might look something like `http://127.0.0.1:5000`, which would redirect you to the application.
    * Option 2: Execute `npm run dev` to start Vite, then follow the link of the link outputed by this command to the browser (it might look something like `http://localhose:...`).

For the differences between these two start options are explained in later sections.

## Directory Structure Explanation

The `app.py` defines the backend stuffs, using the models, data in `data` (I don't know how to name this folder for now).

The `src` hosts the React codes of this project. When running `npm run dev`, the frontend runs from this file (but also communicates to the backend if the backend is running).

The `dist` directory are built from `src` (using the command `npm run build`). When running `python3 app.py`, the base page routes to the `index.html` in this directory.

## Differences Between the Two Running Options

For option 2, any saved changes in the React codes are reflected immediately in the browser; this is Vite's hot module replacement in work.

For option 1, saved changes to the React code would not reflect unless running `npm run build` to build the files in `dist`, but if you are not planning on touching the React part, this wouldn't be too much of a problem.
