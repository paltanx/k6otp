import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.3.0/index.js';

// Parse stages and sleep duration from environment variables
const envConfig = JSON.parse(__ENV.CONFIG || '{"stages": [], "sleep": 1}');
const stages = envConfig.stages;
const sleepDuration = envConfig.sleep;

export const options = {
    stages: stages
};

export default function () {
    const url = __ENV.URL;

    // Generate random userId and userPhoneNumber
    const userId = randomString(20); // Generates a random string of 20 characters
    const userPhoneNumber = "+56958301622";

    const payload = JSON.stringify({
        userId: userId,
        initiative: "remittance",
        userPhoneNumber: userPhoneNumber
    });

    const params = {
        headers: {
            'otp-action': 'CREATE',
            'Content-Type': 'application/json',
        },
    };

    const response = http.post(url, payload, params);

    check(response, {
        'is status 202': (r) => r.status === 202,
    });

    sleep(sleepDuration);
}
