package com.next.codeqz.controller;


import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.UUID;

@Data
@AllArgsConstructor
public class User {
    private UUID id;
    private String email;
    private String password;


}
