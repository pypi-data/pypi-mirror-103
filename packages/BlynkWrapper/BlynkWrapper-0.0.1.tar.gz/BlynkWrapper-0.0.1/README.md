# Python ready to use Blynk Wrapper

## Usage
```PYTHON
from BlynkWrapper.Wrapper import BlynkWrapper
blynk = BlynkWrapper("yourAuthToken", "domainNameOrIPAddressOfBlynkServer", debug=True)

blynk.getStyledButtons()


blynk.getDevices()
```