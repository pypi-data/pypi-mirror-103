from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class CFDI(dict):
    UUID: str
    Fecha: datetime
    Total: Decimal
    # XML fields
    Folio: Optional[str] = None
    Serie: Optional[str] = None
    NoCertificado: Optional[str] = None
    Certificado: Optional[str] = None
    TipoDeComprobante: Optional[str] = None
    LugarExpedicion: Optional[str] = None
    FormaPago: Optional[str] = None
    MetodoPago: Optional[str] = None
    Moneda: Optional[str] = None
    SubTotal: Optional[Decimal] = None
    # CSV Fields
    RfcEmisor: Optional[str] = None
    NombreEmisor: Optional[str] = None
    RfcReceptor: Optional[str] = None
    NombreReceptor: Optional[str] = None
    RfcPac: Optional[str] = None
    FechaCertificacionSat: Optional[datetime] = None
    EfectoComprobante: Optional[str] = None
    Estatus: Optional[str] = None
    FechaCancelacion: Optional[datetime] = None

    def merge(self, other: "CFDI"):
        for attrib, value in self.__dict__.items():
            other_value = getattr(other, attrib)
            if other_value:
                if value and value != other_value:
                    raise ValueError(f"Inconsistent Information '{value}' != '{other_value}'")
                setattr(self, attrib, other_value)
