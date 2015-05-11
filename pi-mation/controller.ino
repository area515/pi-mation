/* 
 Keyboard Message test
 
 For the Arduino Leonardo and Micro.
 
 Sends a text string when a button is pressed.

 The circuit:
 * pushbutton attached from pin 4 to +5V
 * 10-kilohm resistor attached from pin 4 to ground
 
 created 24 Oct 2011
 modified 27 Mar 2012
 by Tom Igoe
 modified 11 Nov 2013
 by Scott Fitzgerald
 modified 11 May 2015
 by Sean O'Bryan
 
 This example code is in the public domain.
 
 http://www.arduino.cc/en/Tutorial/KeyboardMessage
 
 */
// esc
const int escButtonPin = 4;          // input pin for button representing esc key
int escPreviousButtonState = HIGH;   // for checking the state of a escButton

// r
const int rButtonPin = 4;          // input pin for button representing r key
int rPreviousButtonState = HIGH;   // for checking the state of a rButton

// f1
const int f1ButtonPin = 4;           // input pin for button representing f1 key
int f1PreviousButtonState = HIGH;    // for checking the state of a f1Button

// tab
const int tabButtonPin = 4;          // input pin for button representing tab key
int tabPreviousButtonState = HIGH    // for checking the state of a tabButton

// p
const int pButtonPin = 4;          // input pin for button representing p key
int pPreviousButtonState = HIGH    // for checking the state of a pButton

// backspace
const int backspaceButtonPin = 4;          // input pin for button representing backspace key
int backspacePreviousButtonState = HIGH    // for checking the state of a backspaceButton

// enter
const int enterButtonPin = 4;          // input pin for button representing enter key
int enterPreviousButtonState = HIGH    // for checking the state of a enterButton

// space
const int spaceButtonPin = 4;          // input pin for button representing space key
int spacePreviousButtonState = HIGH    // for checking the state of a spaceButton
                  // button push counter

void setup() {
  // make the pushButton pin an input:
  pinMode(buttonPin, INPUT);
  // initialize control over the keyboard:
  Keyboard.begin();
}

void loop() {
	
  // read the escButton:
  int escButtonState = digitalRead(escButtonPin);
    // if the escButton state has changed, and it's currently pressed:
  if ((escButtonState != escPreviousButtonState) && (escButtonState == HIGH)) {
   Keyboard.write((char) 27);
  }
  // save the current escButton state for comparison next time:
  escPreviousButtonState = buttonState;
  
    // read the rButton:
  int rButtonState = digitalRead(rButtonPin);
    // if the rButton state has changed, and it's currently pressed:
  if ((rButtonState != rPreviousButtonState) && (rButtonState == HIGH)) {
   Keyboard.write((char) 114);
  }
  // save the current rButton state for comparison next time:
  rPreviousButtonState = rButtonState;
  
  // read the f1Button:
  int f1ButtonState = digitalRead(f1ButtonPin);
  // if the f1Button state has changed, and it's currently pressed:
  if ((f1ButtonState != f1PreviousButtonState) && (f1ButtonState == HIGH)) {
   Keyboard.set_key2(KEY_F2);
   Keyboard.send_now();
   Keyboard.set_key2(0);
   Keyboard.send_now();
   
  }
  // save the current f1Button state for comparison next time:
  f1PreviousButtonState = f1ButtonState;
  
  // read the tabButton:
  int tabButtonState = digitalRead(tabButtonPin);
  // if the tabButton state has changed, and it's currently pressed:
  if ((tabButtonState != tabPreviousButtonState) && (tabButtonState == HIGH)) {
   Keyboard.write((char) 9);
  }
  // save the current tabButton state for comparison next time:
  tabPreviousButtonState = tabButtonState;
  
  // read the pButton:
  int pButtonState = digitalRead(pButtonPin);
  // if the pButton state has changed, and it's currently pressed:
  if ((pButtonState != pPreviousButtonState) && (pButtonState == HIGH)) {
   Keyboard.write((char) 112);
  }
  // save the current pButton state for comparison next time:
  pPreviousButtonState = pButtonState;
  
  // read the backspaceButton:
  int backspaceButtonState = digitalRead(backspaceButtonPin);
  // if the pButton state has changed, and it's currently pressed:
  if ((backspaceButtonState != backspacePreviousButtonState) && (backspaceButtonState == HIGH)) {
   Keyboard.write((char) 8);
  }
  // save the current backspaceButton state for comparison next time:
  backspacePreviousButtonState = backspaceButtonState;
  
    // read the enterButton:
  int enterButtonState = digitalRead(enterButtonPin);
  // if the enterButton state has changed, and it's currently pressed:
  if ((enterButtonState != enterPreviousButtonState) && (enterButtonState == HIGH)) {
   Keyboard.write((char) 13);
  }
  // save the current enterButton state for comparison next time:
  enterPreviousButtonState = enterButtonState;
  
    // read the spaceButton:
  int spaceButtonState = digitalRead(spaceButtonPin);
  // if the spaceButton state has changed, and it's currently pressed:
  if ((spaceButtonState != spacePreviousButtonState) && (spaceButtonState == HIGH)) {
   Keyboard.write((char) 32);
  }
  // save the current spaceButton state for comparison next time:
  spacePreviousButtonState = spaceButtonState;
}
