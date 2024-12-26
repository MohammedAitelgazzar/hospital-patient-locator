package com.app.repositories;



import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;


import com.app.entities.Role;


@Repository
public interface RoleRepository extends JpaRepository<Role, Long> {
    Role findByName(String name);
}
