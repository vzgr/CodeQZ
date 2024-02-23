package com.next.codeqz.dao;

import com.next.codeqz.controller.User;

import java.util.UUID;

public interface UserDao {
    User getUser(UUID id);
    User getUserByEmail(String email);
    void createUser(User user);
    void auth(User user);

}
