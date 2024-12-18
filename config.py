class Config:
    SECRET_KEY = 'test1'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bhattdk19@gmail.com'
    MAIL_PASSWORD = 'lraugnsclxihthkr'
    # SQLALCHEMY_DATABASE_URI='sqlite:///packages.db'
    SQLALCHEMY_DATABASE_URI='postgresql://maachamunda_user:yUtqgY4oelMx3dda39IHdWUnbAT6cZB5@dpg-ctheu123esus73fds840-a.oregon-postgres.render.com/maachamunda'
    # postgresql://maachamunda_user:yUtqgY4oelMx3dda39IHdWUnbAT6cZB5@dpg-ctheu123esus73fds840-a.oregon-postgres.render.com/maachamunda
    SQLALCHEMY_TRACK_MODIFICATIONS= False
