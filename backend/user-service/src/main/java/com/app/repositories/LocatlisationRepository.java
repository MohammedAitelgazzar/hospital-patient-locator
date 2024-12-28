package com.app.repositories;

import com.app.entities.Localisation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface LocatlisationRepository extends MongoRepository<Localisation,String> {

}
