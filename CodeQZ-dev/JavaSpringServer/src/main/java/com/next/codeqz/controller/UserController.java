package com.next.codeqz.controller;

import com.next.codeqz.exceptions.MyAuthException;
import com.next.codeqz.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor

public class UserController {
    private final UserService userService;
    @CrossOrigin(origins = "http://localhost:63342")
    @PostMapping("/auth")
    public ResponseEntity<Void> auth (@RequestBody User user) {
        try {
            userService.auth(user);
            return ResponseEntity.ok().build();
        } catch (MyAuthException e) {
            return ResponseEntity.status(403).build();

        }
    }
    @CrossOrigin(origins = "http://localhost:63342")
    @PostMapping("/reg")
    public ResponseEntity<Void> registration (@RequestBody User user) {
        try {
            userService.addUser(user);
            return ResponseEntity.ok().build();
        } catch (MyAuthException e) {
            return ResponseEntity.status(403).build();

        }
    }
}
