package com.next.codeqz.service;

import com.next.codeqz.controller.User;
import com.next.codeqz.dao.UserDao;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService{
    private final UserDao userDao;
    @Override
    public User getUserById() {
        return null;
    }

    @Override
    public User getByEmail(String email) {
        return userDao.getUserByEmail(email);


    }

    @Override
    public void addUser(User user) {
        userDao.createUser(user);
    }

    @Override
    public void auth(User user) {
        userDao.auth(user);
    }
}
