1- 
@app.on_event("startup")
async def startup_event():
    logger.info("SERVER-B starting up")
why async

2- 
    # start log
    logger.debug("Preparing to save IP data to Redis: %s", ip_data.model_dump())
    logger.info("Saving IP %s to Redis with key '%s'", ip_data.ip, key)
    #extract ip to serve as the key
    key = str(ip_data.ip)

    # Save the full object as JSON
    redis_client.set(key, ip_data.model_dump_json())
    logger.info("Successfully saved IP %s to Redis", ip_data.ip)

what is the %s
3- 
how does     logger.info("Saving IP %s to Redis with key '%s'", ip_data.ip, key)
 know the key before its assinged 



4- 
like this 

    # Save the full object as JSON
    try:
        redis_client.set(key, ip_data.model_dump_json())
    except Exception as exc:
        logger.error("Error saving IP %s to Redis: %s", ip_data.ip, exc, exc_info=True)
    
    logger.info("Successfully saved IP %s to Redis", ip_data.ip)
