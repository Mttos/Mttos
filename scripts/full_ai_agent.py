#!/usr/bin/env python3
import os
import sys
import logging
from github import Github

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        """Inicializa el agente IA con GitHub"""
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('GITHUB_REPOSITORY')
        
        if not self.token:
            logger.error("❌ GITHUB_TOKEN no definido")
            sys.exit(1)
        
        if not self.repo_name:
            logger.error("❌ GITHUB_REPOSITORY no definido")
            sys.exit(1)
        
        logger.info(f"✅ Conectando a {self.repo_name}")
        
        try:
            self.g = Github(self.token)
            self.repo = self.g.get_repo(self.repo_name)
            logger.info(f"✅ Conectado a {self.repo.full_name}")
        except Exception as e:
            logger.error(f"❌ Error conectando a GitHub: {e}")
            sys.exit(1)
    
    def detect_task(self, title, body):
        """Detecta el tipo de tarea"""
        text = (title + " " + body).lower()
        
        if any(w in text for w in ["revisar", "review", "bug", "error", "problema"]):
            return "🔍 CODE_REVIEW"
        elif any(w in text for w in ["documentación", "readme", "guía", "manual"]):
            return "📚 DOCUMENTATION"
        elif any(w in text for w in ["resumen", "summary", "análisis"]):
            return "📊 SUMMARY"
        elif any(w in text for w in ["test", "prueba", "testing"]):
            return "🧪 TESTING"
        else:
            return "💭 CUSTOM"
    
    def generate_response(self, task_type, title, body):
        """Genera una respuesta"""
        responses = {
            "🔍 CODE_REVIEW": f"🤖 **AI Agent - CODE REVIEW**\n\n**Issue:** {title}\n\n✅ Analizando código...\n- Estructura y formato\n- Mejores prácticas\n- Posibles optimizaciones\n\n",
            "📚 DOCUMENTATION": f"🤖 **AI Agent - DOCUMENTACIÓN**\n\n**Tema:** {title}\n\n✅ Generando documentación:\n- Descripción\n- Instrucciones\n- Ejemplos\n\n",
            "📊 SUMMARY": f"🤖 **AI Agent - RESUMEN**\n\n**Contenido:** {title}\n\n✅ Resumen generado:\n- Puntos principales\n- Análisis\n- Conclusiones\n\n",
            "🧪 TESTING": f"🤖 **AI Agent - TESTING**\n\n**Código a testear:** {title}\n\n✅ Recomendaciones:\n- Tests unitarios\n- Tests de integración\n- Cobertura\n\n",
            "💭 CUSTOM": f"🤖 **AI Agent - RESPUESTA**\n\n**Tu solicitud:** {title}\n\n✅ Procesando...\n- Analizando\n- Procesando\n- Respondiendo\n\n"
        }
        return responses.get(task_type, responses["💭 CUSTOM"])
    
    def run(self):
        """Ejecuta el agente"""
        logger.info("=" * 60)
        logger.info("🚀 FULL AI AGENT INICIADO")
        logger.info("=" * 60)
        
        try:
            # Obtener issues abiertos
            issues = self.repo.get_issues(state='open')
            latest_issue = next(issues, None)
            
            if not latest_issue:
                logger.info("❌ No hay issues abiertos")
                return
            
            logger.info(f"📋 Procesando Issue #{latest_issue.number}: {latest_issue.title}")
            
            # Detectar tipo de tarea
            task_type = self.detect_task(latest_issue.title, latest_issue.body or "")
            logger.info(f"🎯 Tipo detectado: {task_type}")
            
            # Generar respuesta
            response = self.generate_response(task_type, latest_issue.title, latest_issue.body or "")
            
            # Publicar comentario
            try:
                latest_issue.create_comment(response)
                logger.info(f"✅ Comentario publicado en Issue #{latest_issue.number}")
            except Exception as e:
                logger.error(f"❌ Error publicando comentario: {e}")
                return
            
            logger.info("=" * 60)
            logger.info("✅ AGENTE COMPLETADO EXITOSAMENTE")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Error en agente: {e}")
            sys.exit(1)

if __name__ == "__main__":
    agent = AIAgent()
    agent.run()
