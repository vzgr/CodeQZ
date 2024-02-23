package com.next.codeqz.dao;

import com.next.codeqz.controller.User;
import com.next.codeqz.exceptions.MyAuthException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
@Slf4j
@Repository
public class UserDaoImpl implements UserDao{


    private static Map<String, User> usersByEmail = new HashMap();


    static {
        UUID adminId = UUID.randomUUID();
        UUID userId = UUID.randomUUID();
        User admin = new User(adminId, "sora", "123");
        User user = new User(userId, "user", "321");
        usersByEmail.put("sora", admin);
        usersByEmail.put("user", user);
        log.info("admin id = {}", adminId);
        log.info("user id = {}", userId);
    }
    @Override
    public User getUser(UUID id) {
        return null;
    }

    @Override
    public User getUserByEmail(String email) {
        return null;
    }

    @Override
    public void createUser(User user) {
        UUID id = UUID.randomUUID();
        user.setId(id);
        usersByEmail.put(user.getEmail(), user);
    }

    @Override
    public void auth(User user) {
        User authUser = usersByEmail.get(user.getEmail());
        if (authUser == null) {
            throw new MyAuthException();
        }
        if (!authUser.getPassword().equals(user.getPassword())) {
            throw new MyAuthException();
        }
    }
}
