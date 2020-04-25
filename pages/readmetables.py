# this is just the text of the about the team table in raw html to be imported

team = '''
  <table width=100%>
    <tr>
      <td><a href='https://github.com/eyvonne'>Eyve Geordan</a></td>
      <td><a href='https://github.com/jtsheppard'>J Tyler Sheppard</a></td>
      <td><a href='https://github.com/ash12hub'>Ashwin Swamy</a></td>
      <td><a href='https://github.com/hurshd0'>Harsh Desai</a></td>
      <tr>
        <td><a href='https://github.com/eyvonne'><img src='https://media-exp1.licdn.com/dms/image/C5603AQFERauBl6COOA/profile-displayphoto-shrink_200_200/0?e=1593043200&v=beta&t=aYaek2d2OEW_E5NJW52LvbM6XUBY5GLHXzA9-GMY1c8'></a></td>
        <td><a href='https://github.com/jtsheppard'><img src='https://media-exp1.licdn.com/dms/image/C4E03AQGF_MRS5-sEFw/profile-displayphoto-shrink_200_200/0?e=1593043200&v=beta&t=hYIR_Dfb7OB5M1kLJWzVZAcJIbFH_k6CPmg7MUy7woQ'></a></td>
        <td><a href='https://github.com/ash12hub'><img src='https://raw.githubusercontent.com/quake-labs/quake-ds/master/ashwin.jpg'></a></td>
        <td><a href='https://github.com/hurshd0'><img src='https://media-exp1.licdn.com/dms/image/C4E03AQGYKgdNlcItIg/profile-displayphoto-shrink_200_200/0?e=1593043200&v=beta&t=DbV2KbYDHIDvpoz3r3Cv0MWj6ThZGzQtYu71JEMf7PY'></a></td>
      </tr>
          <td><a href='https://github.com/eyvonne'><img src='https://github.com/favicon.ico'></a></td>
          <td><a href='https://github.com/jtsheppard'><img src='https://github.com/favicon.ico'></a></td>
          <td><a href='https://github.com/ash12hub'><img src='https://github.com/favicon.ico'></a></td>
          <td><a href='https://github.com/hurshd0'><img src='https://github.com/favicon.ico'></a></td>
    </tr>
        <td><a href='https://www.linkedin.com/in/eyvonne-geordan-2a2b55168/'><img src='https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca'></a></td>
        <td><a href='https://www.linkedin.com/in/jtsheppard/'><img src='https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca'></a></td>
        <td><a href='https://www.linkedin.com/'><img src='https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca'></a></td>
        <td><a href='https://www.linkedin.com/in/hurshd/'><img src='https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca'></a></td>
    '''


routes = '''
  <table cellpadding='5' border='1'>
    <tr>
      <td>Method</td>
      <td>Endpoint</td>
      <td>Access Control</td>
      <td>Description</td>
      <tr>
        <td>GET</td>
        <td>`/lastQuake/SOURCE/MAGNITUDE`</td>
        <td>Public</td>
        <td>Returns the last quake over the given magnitude from the source</td>
      </tr>
      <td>GET</td>
      <td>`/last/SOURCE/TIME/MAGNITUDE`</td>
      <td>Public</td>
      <td>Gets the quakes over the given timeframe</td>
    </tr>
    <td>GET</td>
    <td>`/history/SOURCE/LAT,LON,DIST`</td>
    <td>Public</td>
    <td>Returns all quakes in a given area</td>
    </tr>
    <td>GET</td>
    <td>`/zip/ZIPCODE/DIST`</td>
    <td>Public</td>
    <td>Returns last quake in a given area</td>
'''
