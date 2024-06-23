package com.example.edital.repository;

import com.example.edital.model.Edital;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EditalRepository extends JpaRepository<Edital, Long> {
}
