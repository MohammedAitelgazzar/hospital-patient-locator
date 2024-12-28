package com.app.entities;


import jakarta.persistence.Id;
import lombok.*;
import org.springframework.data.mongodb.core.mapping.Document;

<<<<<<< HEAD
import java.time.LocalDateTime;

=======
>>>>>>> 1bf2644cb12b230da951345c768947ff95ac64e7
@Document(collection = "localisations")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Localisation {

<<<<<<< HEAD
    @Id
    private String id;

    private String username;

    private LocalDateTime createdAt;


=======
    private String room_id;

    private String username;

>>>>>>> 1bf2644cb12b230da951345c768947ff95ac64e7
}
