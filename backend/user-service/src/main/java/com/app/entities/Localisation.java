package com.app.entities;


import jakarta.persistence.Id;
import lombok.*;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "localisations")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Localisation {

    private String room_id;

    private String username;

}
