import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.modules.transactions.exception import DomainException

logging.basicConfig(
    filename='logs_erros.log', 
    level=logging.ERROR, 
    encoding='utf-8'
)

logger = logging.getLogger(__name__)

def register_error_handlers(app: FastAPI) -> None:
    
    # Captura os erros esperados Execption (NotFound, BadRequest)
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        logger.error(
            f"Erro de Domínio: \n\nCodigo de error: [{exc.error_code}] \n\nMessage de error: {exc.message} \n\nContexto: {exc.context}"
        )
        
        response_content = {
            "error_code": exc.error_code,
            "message": exc.message,
            "context": exc.context if exc.context else {} 
        }
            
        return JSONResponse(
            content=jsonable_encoder(response_content),
            status_code=exc.status_code
        )

    # Captura qualquer erro inesperado (queda de banco, erros de tipo do Python, bugs de logica)
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Erro crítico não tratado no servidor: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "Ocorreu um erro interno inesperado no servidor. Tente novamente mais tarde."
            }
        )
