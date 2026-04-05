#include <stdio.h>
#include <stdbool.h>

/* Safety constants */
const float TORQUE_THRESHOLD_NM = 2.2f;
const float BATTERY_MIN_V = 3.4f;

/* Lock States */
typedef enum {
    UNLOCKED,
    PRE_LOCKED,
    LOCKED
} LockState;

/* Sensor status */
typedef struct {
    float torque_nm;
    float battery_v;
    bool consent_given;
    bool strap_buckle_unlatched;
    bool mouth_cap_removed;
    bool lock_disabled;
} DeviceStatus;

LockState current_state = UNLOCKED;
DeviceStatus status = {0.0f, 0.0f, false, false, false, false};

/**
 * Perform the battery health check.
 * If battery voltage < 3.4V, set lock_disabled flag.
 */
void check_battery_health(float voltage) {
    status.battery_v = voltage;
    if (voltage < BATTERY_MIN_V) {
        status.lock_disabled = true;
    } else {
        status.lock_disabled = false;
    }
}

/**
 * Handle the dual-release mechanism.
 * If either the strap buckle is unlatched or the mouth cap is removed,
 * the lock must release immediately (fail-open logic).
 */
bool check_dual_release_triggered(bool buckle_unlatched, bool mouth_removed) {
    status.strap_buckle_unlatched = buckle_unlatched;
    status.mouth_cap_removed = mouth_removed;

    // Hard-coded safety: any trigger releases the lock
    if (buckle_unlatched || mouth_removed) {
        return true;
    }
    return false;
}

/**
 * Update the solenoid state based on the current lock state.
 * Ensure fail-open behavior: solenoid is only energized in LOCKED state.
 */
void update_solenoid(LockState state) {
    if (state == LOCKED) {
        // ENERGIZE SOLENOID (engage lock)
        // Note: Hardware uses a pull-down resistor to fail-open
        // gpio_set_level(SOLENOID_PIN, 1);
    } else {
        // RELEASE SOLENOID (unlock)
        // gpio_set_level(SOLENOID_PIN, 0);
    }
}

/**
 * Core state machine for lock control.
 */
void update_lock_state(float torque_nm, bool consent) {
    status.torque_nm = torque_nm;
    status.consent_given = consent;

    // Safety Override: Battery low or dual-release triggered
    if (status.lock_disabled || status.strap_buckle_unlatched || status.mouth_cap_removed) {
        current_state = UNLOCKED;
        update_solenoid(current_state);
        return;
    }

    switch (current_state) {
        case UNLOCKED:
            if (torque_nm >= TORQUE_THRESHOLD_NM && consent) {
                current_state = PRE_LOCKED;
            }
            break;
        case PRE_LOCKED:
            if (torque_nm >= TORQUE_THRESHOLD_NM && consent) {
                current_state = LOCKED;
            } else if (torque_nm < TORQUE_THRESHOLD_NM) {
                current_state = UNLOCKED;
            }
            break;
        case LOCKED:
            // Remain locked unless safety override or deliberate release (not implemented in this core logic)
            break;
    }

    update_solenoid(current_state);
}
