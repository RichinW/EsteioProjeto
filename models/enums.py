import enum

class StatusVerification(enum.Enum):
    Corridigo = 'Corrigido'
    Errado = 'Errado'
    Certo = 'Certo'


class StatusConservation(enum.Enum):
    C1 = 'Bom estado'
    C2 = 'Mau estado'
    C3 = 'Danificado'
    C4 = 'Vandalizado'
    C5 = 'Ausente'


class ConservationObservation(enum.Enum):
    C11 = 'Pequena avaria'
    C21 = 'Obstruido pela vegetação'
    C22 = 'Sujo'
    C31 = 'Amassado'
    C32 = 'Condições de fixação inadequadas'
    C33 = 'Película avariada'
    C34 = 'Enferrujado'
    C41 = 'Pichado'
    C42 = 'Riscado'
    C43 = 'Marca de tiro'
    C44 = 'Adesivo'
    C51 = 'Ausente'