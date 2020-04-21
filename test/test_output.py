from graviteeio_cli.graviteeio.output import OutputFormatType

#APIS_PS_DATA = [['339ac63d-a072-4234-9ac6-3da0726234be', 'Gravitee.io features', '<none>', '\x1b[32mV\x1b[0m', '\x1b[32mSTARTED\x1b[0m'], ['1a5b26e9-d7b9-4990-9b26-e9d7b90990c2', 'Gravitee.io Portal Rest API', '<none>', '\x1b[32mV\x1b[0m', '\x1b[32mSTARTED\x1b[0m'], ['b3079628-14ad-451b-8796-2814ad751baa', 'Issue 357', '<none>', '\x1b[33mX\x1b[0m', '\x1b[31mSTOPPED\x1b[0m']]
APIS_PS_DATA = [{'Id': '339ac63d-a072-4234-9ac6-3da0726234be', 'Name': 'Gravitee.io features', 'Tags': [], 'Synchronized': True, 'Status': 'started', 'Workflow': None}]
APIS_PS_DATA_table = [{'Id': '339ac63d-a072-4234-9ac6-3da0726234be', 'Name': 'Gravitee.io features', 'Tags': '<none>', 'Synchronized': '\x1b[32mV\x1b[0m', 'Status': '\x1b[32mSTARTED\x1b[0m'}]

def test_output_dict_table(capsys):
    data = {"param1": "value1","param2": "value2"}
    OutputFormatType.TABLE.echo(data, header = ["Header","Header"])
    captured = capsys.readouterr()
    assert captured.out == " Header  Header \n----------------\n param1  value1 \n param2  value2 \n"

def test_output_list_table(capsys):
    data = ['demo', 'qualif', 'prod']
    OutputFormatType.TABLE.echo(data, header = ["Env"])
    captured = capsys.readouterr()
    assert captured.out == " Env    \n--------\n demo   \n qualif \n prod   \n"

def test_output_list_table_without_header(capsys):
    data = ['demo', 'qualif', 'prod']
    OutputFormatType.TABLE.echo(data)
    captured = capsys.readouterr()
    assert captured.out == "          \n----------\n demo     \n qualif   \n prod     \n"

def test_output_dict_tsv(capsys):
    data = {"param1": "value1","param2": "value2"}
    OutputFormatType.TSV.echo(data, header = ["Header1","Header2"])
    captured = capsys.readouterr()
    assert captured.out == "Header1\tHeader2\nparam1\tvalue1\nparam2\tvalue2\n"

def test_output_list_tsv(capsys):
    data = ['demo', 'qualif', 'prod']
    OutputFormatType.TSV.echo(data, header = ["Env"])
    captured = capsys.readouterr()
    assert captured.out == "Env\ndemo\nqualif\nprod\n"

def test_output_dict_table_apis_ps(capsys):
    OutputFormatType.TABLE.echo(APIS_PS_DATA_table, header = ["id","Name","Tags","Synchronized","Status"])
    captured = capsys.readouterr()
    assert captured.out == " id                                    Name                  Tags    Synchronized  Status  \n-------------------------------------------------------------------------------------------\n 339ac63d-a072-4234-9ac6-3da0726234be  Gravitee.io features  <none>  V             STARTED \n"

def test_output_dict_tsv_apis_ps_with_no_data(capsys):
    OutputFormatType.TSV.echo([], header = [])
    captured = capsys.readouterr()
    assert captured.out == "\t\n"

def test_output_dict_tsv_apis_ps(capsys):
    OutputFormatType.TSV.echo(APIS_PS_DATA, header = ["id","Name","Tags","Synchronized","Status"])
    captured = capsys.readouterr()
    assert captured.out == "id\tName\tTags\tSynchronized\tStatus\n339ac63d-a072-4234-9ac6-3da0726234be\tGravitee.io features\t[]\tTrue\tstarted\tNone\n"

def test_output_dict_json(capsys):
    data = {"param1": "value1","param2": "value2"}
    OutputFormatType.JSON.echo(data)
    captured = capsys.readouterr()
    assert captured.out == "{\n  \"param1\": \"value1\",\n  \"param2\": \"value2\"\n}\n"

def test_output_dict_yaml(capsys):
    data = {"param1": "value1","param2": "value2"}
    OutputFormatType.YAML.echo(data)
    captured = capsys.readouterr()
    assert captured.out == "param1: value1\nparam2: value2\n\n"
