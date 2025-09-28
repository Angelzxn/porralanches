from sqlalchemy import create_engine, Column, UUID, String, Integer, Float, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from config import Config
import uuid

db = create_engine(Config.DATABASE_URL, echo=True, future=True, pool_pre_ping=True)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    nome_completo = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    cpf = Column(String(11), nullable=False, unique=True, index=True)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="cliente", cascade="all, delete-orphan")

    def __init__(self, nome, email, cpf, senha):
        self.nome_completo = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha


class Endereco(Base):
    __tablename__ = "enderecos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False, index=True)
    endereco = Column(String(200), nullable=False)
    complemento = Column(String(200), nullable=False)
    referencia = Column(String(200), nullable=True)
    bairro = Column(String(200), nullable=False)
    cidade = Column(String(200), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(200), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    cliente = relationship("Cliente", back_populates="enderecos")

    def __init__(self, cliente_id, endereco, complemento, bairro, cidade, estado, cep, referencia = None):
        self.cliente_id = cliente_id
        self.endereco = endereco
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.referencia = referencia

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    titulo = Column(String(200), nullable=False)
    razao_social = Column(String(200), nullable=False)
    cnpj = Column(String(14), nullable=False)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=False, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    lojas = relationship("Loja", back_populates="empresa", cascade="all, delete-orphan")

    def __init__(self, titulo, razao_social, cnpj, senha):
        self.titulo = titulo
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.senha = senha


class Loja(Base):
    __tablename__ = "lojas"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False, index=True)
    senha = Column(String, nullable=False)
    titulo = Column(String(200), nullable=False)
    cidade = Column(String(200), nullable=False, index=True)
    estado = Column(String(2), nullable=False, index=True)
    logo = Column(String, nullable=False)
    ativo = Column(Boolean, default=False, nullable=False)
    pedido_min = Column(Float, nullable=False)
    taxa_entrega = Column(Float, default=0, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    empresa = relationship("Empresa", back_populates="lojas")
    produtos = relationship("Produto", back_populates="loja", cascade="all, delete-orphan")
    carrinhos = relationship("Carrinho", back_populates="loja", cascade="all, delete-orphan")


class Produtos(Base):
    __tablename__ = "produtos"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    loja_id = Column(UUID(as_uuid=True), ForeignKey("lojas.id"), nullable=False, index=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(String(1000), nullable=False)
    preco_un = Column(Float, nullable=False)
    preco_un_promocional = Column(Float, nullable=True)
    em_promocao = Column(Boolean, default=False, nullable=False)
    ativo = Column(Boolean, nullable=False, default=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    fotos = relationship("ProdutoFoto", back_populates="produto", cascade="all, delete-orphan")
    loja = relationship("Loja", back_populates="produtos")
    carrinhos = relationship("ProdutoCarrinho", back_populates="produto", cascade="all, delete-orphan")


class ProdutoFoto(Base):
    __tablename__ = "produtos_fotos"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    produto_id = Column(UUID(as_uuid=True), ForeignKey("produtos.id"), index=True)
    caminho = Column(String, nullable=False)
    main = Column(Boolean, nullable=False, default=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    produto = relationship("Produto", back_populates="fotos")


class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    loja_id = Column(UUID(as_uuid=True), ForeignKey("lojas.id"), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    cliente = relationship("Cliente", back_populates="carrinhos")
    produtos = relationship("ProdutoCarrinho", back_populates="carrinho", cascade="all, delete-orphan")
    loja = relationship("Loja", back_populates="carrinhos")
    pedido = relationship("Pedido", back_populates="carrinho")


class ProdutoCarrinho(Base):
    __tablename__ = "produtos_carrinhos"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    carrinho_id = Column(UUID(as_uuid=True), ForeignKey("carrinhos.id"), nullable=False)
    produto_id = Column(UUID(as_uuid=True), ForeignKey("produtos.id"), nullable=False)
    qtd = Column(Integer, nullable=False, default=1)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    carrinho = relationship("Carrinho", back_populates="produtos")
    produto = relationship("Produtos", back_populates="carrinhos")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    carrinho_id = Column(UUID(as_uuid=True), ForeignKey("carrinhos.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    valor = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="Aguardando pagamento")
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    carrinho = relationship("Carrinho", back_populates="pedido")
    cliente = relationship("Cliente", back_populates="pedidos")