import requests
import fire

def main(url, text=None):
    if text is None:
        text = "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very close to the Manhattan Bridge."
    url_response = requests.post(url, data=text)
    # print(url_response)
    entites = url_response.json()

    print("\nTest string: \n" + text)
    print("\nPredictions: \n")
    print(entites[1:-1])

if __name__ == "__main__":
    fire.Fire(main)