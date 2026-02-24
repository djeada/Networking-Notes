# Data Link Layer

## 1. **Flow Control**
   - **Sender's Window Size**: \(N\). (In Selective Repeat, both sender and receiver window sizes are the same)
   - \(a = \frac{T_p}{T_t}\)

   ![Flow Control Image](images/media/image5.jpg)

   - **Conditions**:
     - Sequence No. ≥ (Sender's Window Size) + (Receiver's Window Size)

## 2. **Efficiency in Time Division Multiplexing (TDM) (Polling)**
   - Efficiency = \(\frac{T_t}{T_{\text{poll}} + T_t}\)

## 3. **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**
   - \(T_t \geq 2 \cdot T_p\)
   - Minimum frame length = \(2 \cdot T_p \cdot B\)
   - Efficiency = \(\frac{1}{1 + 6.44a}\)

## 4. **Back-off Algorithm for CSMA/CD**
   [Back-off Algorithm for CSMA/CD](https://www.geeksforgeeks.org/back-off-algorithm-csmacd/)
   - Waiting time = back–off time
   - Let \(n\) = collision number or re-transmission serial number.
   - Waiting time = \(K \cdot T_{\text{slot}}\)
   - Where \(K\) = \[0, \(2^n – 1\)\]

## 5. **Token Ring**
   - **Early Token Reinsertion**: Efficiency = \(\frac{1}{1 + \frac{a}{N}}\)
   - **Delayed Token Reinsertion**: Efficiency = \(\frac{1}{1 + \frac{(N+1)a}{N}}\)

## 6. **Aloha**
   - Pure Aloha Efficiency = 18.4%
   - Slotted Aloha Efficiency = 36.8%

## 7. **Maximum Data Rate (Channel Capacity)**
   [Maximum Data Rate for Noiseless and Noisy Channels](https://www.geeksforgeeks.org/computer-network-maximum-data-rate-channel-capacity-noiseless-noisy-channels/)
   - **Noiseless Channel: Nyquist Bit Rate**
     - BitRate = \(2 \cdot \text{Bandwidth} \cdot \log_2(L)\)
       - \(L\): Number of signal levels used to represent data.
   - **Noisy Channel: Shannon Capacity**
     - Capacity = \(\text{Bandwidth} \cdot \log_2(1 + \text{SNR})\)
       - SNR: Signal-to-noise ratio

## 8. **Error Control**
   - **Hamming Code**
     [Hamming Code](https://www.geeksforgeeks.org/computer-network-hamming-code/)
     - Used for error-correction to detect and correct errors during data transmission.
     - **Redundant bits**: \(2^r \geq m + r + 1\)
       - \(r\): Redundant bit, \(m\): Data bit
   - **Framing in Data Link Layer (DLL)**
     [Framing in DLL](https://www.geeksforgeeks.org/computer-network-framing-data-link-layer/)
     - Provides a way for a sender to transmit a set of bits that are meaningful to the receiver.
     - **Character/Byte Stuffing**: Used when frames consist of characters. A byte is stuffed into data to differentiate it from the end delimiter (ED).
     - **Bit stuffing**: The sender stuffs a bit to break the pattern, e.g., appends a 0 in data = 0111**0**1.
