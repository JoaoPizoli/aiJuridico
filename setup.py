import subprocess

def main():
    #subprocess.run("echo 'ok1'", shell=True, capture_output=True, text=True)
    #subprocess.run("poetry lock", shell=True, capture_output=True, text=True)
    #subprocess.run("echo 'ok2'", shell=True, capture_output=True, text=True)
    #subprocess.run("poetry install", shell=True, capture_output=True, text=True)
    #subprocess.run("echo 'ok3'", shell=True, capture_output=True, text=True)
    #subprocess.run("poetry show --tree >> poetry.tree", shell=True, capture_output=True, text=True) 
    #subprocess.run("echo 'ok4'", shell=True, capture_output=True, text=True)
    subprocess.run("streamlit run ./src/gui/app.py", shell=True, capture_output=True, text=True)
    #subprocess.run("echo 'ok5'", shell=True, capture_output=True, text=True)

    #subprocess.run("curl -s http://localhost:8502 | curl -X POST https://jusai-br4.streamlit.app/ -d @-", shell=True, capture_output=True, text=True)
    #subprocess.run("echo 'ok6'", shell=True, capture_output=True, text=True)
    #subprocess.run("nohup streamlit run ./src/gui/app.py &", shell=True, capture_output=True, text=True)
    #subprocess.run("nc -l localhost 8501 | nc target_address target_port", shell=True, capture_output=True, text=True)
    #subprocess.run("python src/gui/app.py", shell=True, capture_output=True, text=True)

if __name__ == "__main__":
    main()