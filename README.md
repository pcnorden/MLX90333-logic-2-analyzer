# MLX90333-logic2-decoder

This is a High-Level decoder for the Logic 2 software that [Saleae](https://www.saleae.com/) is making for their logic analyzers.

This is just a personal project that will always be a bit on the sideburner, but I personally use this plugin to decode the magnetic sensor in a Saitec/Logitech (Logitech now owns Saitec) x56 HOTAS joystick and so far I've generally found the library is producing satisfying results regarding reading the data from the sensor inside. More advanced features might come later since right now I just needed the positional data decoded.

If you have any need for more features, please open a issue and I will try to actually implement it into the decoder.

**BEWARE!** This only supports SPI connection to the MLX90333 chip! Saleae's documentation is unfortunately in quite a bad state regarding the analog section, so I really didn't want to spend days trying to puzzle together the analog API for Logic 2
