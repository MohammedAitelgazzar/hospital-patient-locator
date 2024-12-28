package com.app.entities;


import jakarta.persistence.Id;
import lombok.*;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Document(collection = "localisations")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Localisation {

    @Id
    private String id;

    private String username;

    private LocalDateTime createdAt;


}
