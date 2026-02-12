from app.utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Logger initialized")

print("\n" + "="*60)
print("TESTING LOGGER - Watch console AND check logs/ folder")
print("="*60 + "\n")

logger.debug("🔍 This is DEBUG - detailed info for developers")
logger.info("ℹ️  This is INFO - normal operation")
logger.warning("⚠️  This is WARNING - something suspicious")
logger.error("❌ This is ERROR - something failed")
logger.critical("🚨 This is CRITICAL - app is dying!")