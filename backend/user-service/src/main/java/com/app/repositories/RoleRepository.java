package com.app.repositories;



import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;



import com.app.entities.Role;


@Repository
public interface RoleRepository extends MongoRepository<Role, String> {
    Role findByName(String name);
}
