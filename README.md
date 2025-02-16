# Dorbell.env

Version modificada del timbre  este carga las keys para las API con python-ldotenv

# Software y hardware empleado

- Hacemos uso de python y las siguinetes libreias:
    
    * flask
    * requests
    * python-dotenv

- Cuenta en pythonanywhere
- Hemos de crear cuentra en sinricpro y configurar un dispositivo swicht dorbell 
- Como hardware estoy empleando un altavoz xiaomi smart speaker l05g
- Con este metodo no es necesario esp32 ni arduino....

# Como funciona

Como veis hay un fronted y un backend , desde el fronted se genera una peticion al backend el cual la reenvia a la api de sinricpro y activa el timbre que me avisa en el altavoz.

# Como usarlo

Descargais el repo y os creais un fichero .env con el siguiente contenido.

SINRIC_API_KEY=TU API KEY
SINRIC_DEVICE_ID= ID DEL DISPOSITIVO
SINRIC_PORTAL_ID=que lo mas logico seria portal
SINRIC_TOKEN_ID=tu token

Con todo ya preparado lo subis a pythonanywhere y configurais como indica pythonanywhere.

P.D.:Yo no encontraba el TOKEN directamente en la web de sinric, asi que me puse a capturar la peticion que se hace desde la web  al presionar el timbre ahi os debe aparecer como TOKEN BEARER.