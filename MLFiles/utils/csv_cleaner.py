import pandas as pd


def get_studenti_corso(*, attr, corso):
    """
    Ritorna una lista con i Codici Fiscali di tutti gli studenti di uno specifico corso di studio
    :param attr: nome dell'attributo da filtrare. Gestiti solo "des_corso" e "cod_corso" (per ora)
    :param corso: Descrizione del corso di studio (es. "INFORMATICA").
    :return: pandas DataFrame con le righe filtrate secondo il corso di studio selezionato
    """
    ds = pd.read_csv('../files/last_active_students.csv', sep=';')

    if attr=="des_corso" or attr=="cod_corso":
        df = ds.loc[ds[attr] == corso]
    else:
        print("Tipo non gestito: Ritorna None")
        return None

    if df.empty:
        print("Nessun Risultato. Ritorna None")
        return None

    print("Lunghezza dataset: %d righe" %len(df.index))
    return df

