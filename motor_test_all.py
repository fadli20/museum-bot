#!/usr/bin/env python3
"""
Motor Test Script – Individual & Simultaneous
---------------------------------------------
Tests each motor forward/backward individually, then all together.
Uses PWM on enable pins for speed control.

Pin mapping (BCM):
  Motor 1 (Front Left):  IN1=17, IN2=27, EN=22
  Motor 2 (Front Right): IN1=23, IN2=24, EN=25
  Motor 3 (Rear Left):   IN1=5,  IN2=6,  EN=13
  Motor 4 (Rear Right):  IN1=19, IN2=26, EN=16
"""

import RPi.GPIO as GPIO
import time
import sys

# Motor configuration
MOTORS = {
    1: {'name': 'Front Left',  'in1': 17, 'in2': 27, 'en': 22},
    2: {'name': 'Front Right', 'in1': 23, 'in2': 24, 'en': 25},
    3: {'name': 'Rear Left',   'in1': 5,  'in2': 6,  'en': 13},
    4: {'name': 'Rear Right',  'in1': 19, 'in2': 26, 'en': 16},
}

PWM_FREQ = 1000      # 1 kHz
DEFAULT_DUTY = 50    # 50% speed
TEST_DURATION = 2    # seconds per direction

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for m in MOTORS.values():
        GPIO.setup(m['in1'], GPIO.OUT)
        GPIO.setup(m['in2'], GPIO.OUT)
        GPIO.setup(m['en'], GPIO.OUT)
        # Start with all pins LOW (motors off)
        GPIO.output(m['in1'], GPIO.LOW)
        GPIO.output(m['in2'], GPIO.LOW)
        GPIO.output(m['en'], GPIO.LOW)

def cleanup_gpio():
    GPIO.cleanup()

def set_motor(motor_num, direction, duty):
    """
    direction: 'forward', 'backward', or 'stop'
    duty: 0-100 (PWM duty cycle)
    Returns PWM object (or None if stopped).
    """
    m = MOTORS[motor_num]
    # Set direction pins
    if direction == 'forward':
        GPIO.output(m['in1'], GPIO.HIGH)
        GPIO.output(m['in2'], GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(m['in1'], GPIO.LOW)
        GPIO.output(m['in2'], GPIO.HIGH)
    else:  # stop
        GPIO.output(m['in1'], GPIO.LOW)
        GPIO.output(m['in2'], GPIO.LOW)
        GPIO.output(m['en'], GPIO.LOW)
        return None

    # Create PWM on enable pin
    pwm = GPIO.PWM(m['en'], PWM_FREQ)
    pwm.start(duty)
    # Small delay to let the signal stabilise
    time.sleep(0.05)
    return pwm

def stop_motor(motor_num):
    """Stop a motor and clean its PWM."""
    m = MOTORS[motor_num]
    GPIO.output(m['in1'], GPIO.LOW)
    GPIO.output(m['in2'], GPIO.LOW)
    GPIO.output(m['en'], GPIO.LOW)

def test_individual(duration=TEST_DURATION, duty=DEFAULT_DUTY):
    print("\n" + "=" * 50)
    print("INDIVIDUAL MOTOR TESTS")
    print("=" * 50)
    for num in range(1, 5):
        name = MOTORS[num]['name']
        print(f"\n▶ Testing {name} (Motor {num})")
        # Forward
        print(f"  → Forward at {duty}% PWM for {duration}s")
        pwm = set_motor(num, 'forward', duty)
        time.sleep(duration)
        if pwm:
            pwm.stop()
            stop_motor(num)
        # Backward
        print(f"  → Backward at {duty}% PWM for {duration}s")
        pwm = set_motor(num, 'backward', duty)
        time.sleep(duration)
        if pwm:
            pwm.stop()
            stop_motor(num)
        # Stop
        stop_motor(num)
        print("  ✓ Motor stopped")

def test_simultaneous(duration=TEST_DURATION, duty=DEFAULT_DUTY):
    print("\n" + "=" * 50)
    print("SIMULTANEOUS MOTOR TESTS")
    print("=" * 50)

    print(f"\n▶ All motors forward at {duty}% PWM for {duration}s")
    pwms = []
    for num in range(1, 5):
        pwm = set_motor(num, 'forward', duty)
        pwms.append(pwm)
    time.sleep(duration)
    for i, pwm in enumerate(pwms):
        num = i + 1
        if pwm:
            pwm.stop()
        stop_motor(num)

    print(f"\n▶ All motors backward at {duty}% PWM for {duration}s")
    pwms = []
    for num in range(1, 5):
        pwm = set_motor(num, 'backward', duty)
        pwms.append(pwm)
    time.sleep(duration)
    for i, pwm in enumerate(pwms):
        num = i + 1
        if pwm:
            pwm.stop()
        stop_motor(num)

    print("\n✅ All motors stopped")

def main():
    try:
        setup_gpio()
        print("\n" + "=" * 50)
        print("MOTOR TEST SCRIPT")
        print("=" * 50)
        print("This will test each motor individually (forward/backward),")
        print("then all motors together (forward/backward).")
        print("\n⚠️  Make sure wheels are off the ground or the robot")
        print("   is safely secured before continuing!")
        print("=" * 50)

        response = input("Press Enter to start, or 'q' to quit: ").strip().lower()
        if response == 'q':
            cleanup_gpio()
            print("Exited.")
            return

        test_individual()
        test_simultaneous()

        print("\n" + "=" * 50)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user.")
    finally:
        cleanup_gpio()
        print("GPIO cleaned up.")

if __name__ == '__main__':
    main()
