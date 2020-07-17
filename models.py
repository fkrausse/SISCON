class Jogo:
    def __init__(self, cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad, 
    ruc_entidad, forma_pago, importe_total, IVA5, IVA10, IVAexcentos, id=None):
        self.id = id
        self.cta_ingreso = cta_ingreso
        self.cta_egreso = cta_egreso
        self.fecha_factura = fecha_factura
        self.ncomprobante = ncomprobante
        self.nombre_entidad = nombre_entidad
        self.ruc_entidad = ruc_entidad
        self.forma_pago = forma_pago
        self.importe_total = importe_total
        self.IVA5 = IVA5
        self.IVA10 = IVA10
        self.IVAexcentos = IVAexcentos


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
