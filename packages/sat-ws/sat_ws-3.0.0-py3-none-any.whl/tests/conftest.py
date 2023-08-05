# pylint: disable=redefined-outer-name
import random
from datetime import datetime, timedelta
from decimal import Decimal
from importlib import resources
from typing import List

import pytest

from sat.certificate_handler import CertificateHandler
from sat.cfdi import CFDI
from sat.enums import DownloadType, RequestType
from sat.package import Package
from sat.query import Query
from sat.sat_connector import SATConnector
from sat.sat_login_handler import SATLoginHandler

from . import real_fiel

cert = resources.read_binary(real_fiel, "NAPM9608096N8.cer")
key = resources.read_binary(real_fiel, "NAPM9608096N8.key")
password = resources.read_text(real_fiel, "NAPM9608096N8.txt").encode("utf-8")


@pytest.fixture
def certificate_handler():
    new_certificate_handler = CertificateHandler(cert, key, password)
    return new_certificate_handler


@pytest.fixture
def login_handler(certificate_handler):
    _login_handler = SATLoginHandler(certificate_handler)
    return _login_handler


@pytest.fixture
def sat_connector():
    sat_obj = SATConnector(cert, key, password)
    return sat_obj


query_scenarios = [  # TODO make flexible
    (DownloadType.ISSUED, RequestType.CFDI),
    (DownloadType.RECEIVED, RequestType.CFDI),
    (DownloadType.ISSUED, RequestType.METADATA),
    (DownloadType.RECEIVED, RequestType.METADATA),
]


@pytest.fixture(params=query_scenarios)
def query(sat_connector: SATConnector, request):
    start = datetime.fromisoformat("2021-01-01T00:00:00")
    end = datetime.fromisoformat("2021-05-01T00:00:00") + timedelta(
        seconds=random.randint(1, 10000)
    )
    query = Query(request.param[0], request.param[1], start, end)
    query.send(sat_connector)
    return query


@pytest.fixture
def packages(sat_connector: SATConnector, query: Query) -> List[Package]:
    packages = query.get_packages(sat_connector)
    return packages


@pytest.fixture
def zip_cfdi() -> bytes:
    with open("tests/downloads/B2A5BB69-D460-4FAD-8482-6E5E2E81843A_01.zip", "rb") as zipfile:
        content = zipfile.read()
        return content


@pytest.fixture
def zip_metadata() -> bytes:
    with open("tests/downloads/195B748C-0091-4558-8DE8-9A37CBA3F42A_01.zip", "rb") as zipfile:
        content = zipfile.read()
        return content


@pytest.fixture
def cfdi_xml_example() -> CFDI:
    cfdi_example = CFDI(
        UUID="FB657B83-4C66-4B45-A352-97BBCA9C1130",
        Folio="1",
        Serie="RINV/2021/",
        NoCertificado="00001000000503989239",
        Certificado="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",
        TipoDeComprobante="E",
        Fecha=datetime(2021, 2, 23, 15, 51, 25),
        LugarExpedicion="44259",
        FormaPago="03",
        MetodoPago="PUE",
        Moneda="MXN",
        SubTotal=Decimal("25000.00"),
        Total=Decimal("29000.00"),
    )
    return cfdi_example


@pytest.fixture
def cfdi_metadata_example() -> CFDI:
    cfdi_example = CFDI(
        UUID="FB657B83-4C66-4B45-A352-97BBCA9C1130",
        Fecha=datetime(2021, 2, 23, 15, 51, 25),
        Total=Decimal("29000"),
        RfcEmisor="NAPM9608096N8",
        NombreEmisor="Navarro Presas Moisés Alejandro",
        RfcReceptor="PGD1009214W0",
        NombreReceptor="PLATAFORMA GDL S  DE RL DE CV",
        RfcPac="CVD110412TF6",
        FechaCertificacionSat=datetime(2021, 2, 23, 15, 51, 27),
        EfectoComprobante="E",
        Estatus="0",
        FechaCancelacion=datetime(2021, 2, 24, 21, 4, 42),
    )
    return cfdi_example


@pytest.fixture
def cfdi_merge_example() -> CFDI:
    cfdi_example = CFDI(
        UUID="FB657B83-4C66-4B45-A352-97BBCA9C1130",
        Folio="1",
        Serie="RINV/2021/",
        NoCertificado="00001000000503989239",
        Certificado="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",
        TipoDeComprobante="E",
        Fecha=datetime(2021, 2, 23, 15, 51, 25),
        LugarExpedicion="44259",
        FormaPago="03",
        MetodoPago="PUE",
        Moneda="MXN",
        SubTotal=Decimal("25000.00"),
        Total=Decimal("29000.00"),
        RfcEmisor="NAPM9608096N8",
        NombreEmisor="Navarro Presas Moisés Alejandro",
        RfcReceptor="PGD1009214W0",
        NombreReceptor="PLATAFORMA GDL S  DE RL DE CV",
        RfcPac="CVD110412TF6",
        FechaCertificacionSat=datetime(2021, 2, 23, 15, 51, 27),
        EfectoComprobante="E",
        Estatus="0",
        FechaCancelacion=datetime(2021, 2, 24, 21, 4, 42),
    )
    return cfdi_example
