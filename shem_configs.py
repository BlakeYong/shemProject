class Config:
    # JWT 관련
    JWT_SECRET_KEY = 'aiShemwayswinning'
    JWT_ALGORITHM = 'HS256'

    # 배포, DB 관련
    prod_db_schema = 'shem'
    prod_db_host = "18.209.179.23"
    prod_db_user= "shem"
    prod_db_passwd= 'shem1234!'

    access_key= ''
    secret_key= ''
    prod_bucket_name=''
    aws_access_key_id='AKIATGH4KM5RTAUGB65M'
    aws_secret_access_key='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'
    URLS = {
        'error' : 'https=//discordapp.com/api/webhooks/719874016235487274/5QVLpWN7fcS2tnCu3EcAFB7I5G_vIT67whp8afUqsu7tHTKH0G1fN5Nrv90aZehJlJC',
        'log' : 'https=//discordapp.com/api/webhooks/740545340993700001/PyCJxnovkKEePuU6R-bRQ1bhIXsuP-Te_paI3qoUib5721X-kJRu8hxSHzwplY9gjmvM'
    }
    google_maps_key='AIzaSyClekaO67OnHHHj2shK0xz4LhomNx39_k8'
    google_maps_url='https=//maps.googleapis.com/maps/api/directions/json?'