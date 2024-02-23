package com.next.codeqz.service;

import com.next.codeqz.controller.User;

public interface UserService {
    User getUserById();
    User getByEmail(String email);
    void addUser(User user);

    void auth(User user);

}
