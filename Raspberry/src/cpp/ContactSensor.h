#ifndef CONTACTSENSOR_H
#define CONTACTSENSOR_H


class ContactSensor{
    public:
        ContactSensor();
        ~ContactSensor();
        int read_contact_sensor();
};
        
#endif