package com.example.edital.service;

import com.example.edital.model.Edital;
import com.example.edital.repository.EditalRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class EditalService {

    @Autowired
    private EditalRepository editalRepository;

    public List<Edital> getAllEditais() {
        return editalRepository.findAll();
    }

    public Optional<Edital> getEditalById(Long id) {
        return editalRepository.findById(id);
    }

    public Edital saveEdital(Edital edital) {
        return editalRepository.save(edital);
    }

    public void deleteEdital(Long id) {
        editalRepository.deleteById(id);
    }
}
