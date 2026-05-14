from etl.etl_pipeline import run_etl
from models.train_model import train_model
from models.forecast import generate_forecast

def main():

    print("PIPELINE INICIADO")

    run_etl()

    train_model()

    generate_forecast()

    print("PIPELINE FINALIZADO")

if __name__ == "__main__":
    main()
