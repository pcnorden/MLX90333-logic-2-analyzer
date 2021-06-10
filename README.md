# MLX90333 Logic 2 analyzer

![image](https://user-images.githubusercontent.com/7767295/121573975-1bdd7b80-ca26-11eb-80f7-3e875ade629b.png)

This is a High-Level decoder for the Logic 2 software that [Saleae](https://www.saleae.com/) is making for their logic analyzers.

This is just a personal project that will always be a bit on the sideburner, but I personally use this plugin to decode the magnetic sensor in a Saitec/Logitech (Logitech now owns Saitec) x56 HOTAS joystick and so far I've generally found the library is producing satisfying results regarding reading the data from the sensor inside. More advanced features might come later since right now I just needed the positional data decoded.

If you have any need for more features, please open a issue and I will try to actually implement it into the decoder.

I've currently just implemented a selection in the menu when changing settings so you can toggle between the XYZ bit toggle since I can't reliably understand how the HOTAS joystick is putting it into a certain mode, but just change the settings if need be and it should be good.

![image](https://user-images.githubusercontent.com/7767295/121574488-9908f080-ca26-11eb-920c-322b9aa7ed7f.png)

**BEWARE!** This only supports SPI connection to the MLX90333 chip! Saleae's documentation is unfortunately in quite a bad state regarding how to select that the decoder can only be used by a certain input analyzer. If documentation from Saleae gets better I will try to improve the script, if nothing else I will some day just sit down and try to just attack the API and write down what I find in another repo here on github.

Just to be clear about the above sentance since I can come off as quite demeaning, Saleae is a nice company and the Logic 2 software is just excellent every time I've used it, but the only bad part for me is the documentation on the API, everything else is just awesome about the software and the product

# Installation instructions

So, to get the most up-to-date install instructions, I highly recommend going over to Saleae's support page located [here](https://support.saleae.com/extensions/installing-extensions#install-extensions-manually) cause they have a up-to-date guide with (at the time of writing this) very good instructions and screenshots of how to install.

To install, just go to the above website, and scroll down a bit to encounter the "Install Extensions Manually" and skip to step 3 and go from there.
