package com.app.repositories;

import com.app.entities.Localisation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.mongodb.repository.MongoRepository;

<<<<<<< HEAD
import java.util.Optional;

public interface LocatlisationRepository extends MongoRepository<Localisation,String> {
    Optional<Localisation> findTopByOrderByCreatedAtDesc();

=======
public interface LocatlisationRepository extends MongoRepository<Localisation,String> {
>>>>>>> 1bf2644cb12b230da951345c768947ff95ac64e7

}
