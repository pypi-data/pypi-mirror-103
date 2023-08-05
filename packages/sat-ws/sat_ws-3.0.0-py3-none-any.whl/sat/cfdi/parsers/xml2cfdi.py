from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Dict, List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from zipfile import ZipFile

from sat.utils import get_attr

from ..cfdi import CFDI
from .cfdi_parser import CFDIParser, MissingData


class XML2CFDI(CFDIParser):
    root_elements: Dict[str, Callable] = {
        "Folio": str,
        "Serie": str,
        "NoCertificado": str,
        "Certificado": str,
        "TipoDeComprobante": str,
        "Fecha": datetime.fromisoformat,
        "LugarExpedicion": str,
        "FormaPago": str,
        "MetodoPago": str,
        "Moneda": str,
        "SubTotal": Decimal,
        "Total": Decimal,
    }

    @classmethod
    def _get_root_data(cls, xml: Element) -> Dict[str, Any]:
        data = {field: caster(get_attr(xml, field)) for field, caster in cls.root_elements.items()}
        return data

    @classmethod
    def parse(cls, xml: Element) -> CFDI:
        data = cls._get_root_data(xml)
        complemento = xml.find("{http://www.sat.gob.mx/cfd/3}Complemento")
        if not complemento:
            raise MissingData("{http://www.sat.gob.mx/cfd/3}Complemento")
        uuid = get_attr(
            complemento.find("{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital"),
            "UUID",
        )
        data["UUID"] = uuid

        cfdi = CFDI(**data)
        return cfdi

    @classmethod
    def _get_xmls(cls, files: List[str]) -> List[Element]:
        xmls = [ElementTree.fromstring(xml_file) for xml_file in files]
        return xmls

    @classmethod
    def parse_zip(cls, zipfile: ZipFile) -> List["CFDI"]:
        xml_files = cls._get_files(zipfile)
        xmls = cls._get_xmls(xml_files)
        return [cls.parse(xml) for xml in xmls]
