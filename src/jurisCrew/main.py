import sys
from JusAI.src.jurisCrew.crews import JusaiCrew


def run():
    print("\n\n########################")
    print("## RESULTADO")
    print("########################\n")

    output = JusaiCrew().crew().kickoff(inputs=None)
    print(output)
    

def train():
    
    inputs = {}
    try:
        JusaiCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    
if __name__ == "__main__":

    run()
