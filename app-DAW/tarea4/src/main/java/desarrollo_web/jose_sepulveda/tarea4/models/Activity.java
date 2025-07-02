package desarrollo_web.jose_sepulveda.tarea4.models;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;

@Entity 
@Table(name = "actividad")
public class Activity {
    @Id
    @SequenceGenerator(
        name = "actividad_sequence",
        sequenceName = "actividad_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "actividad_sequence"
    )
    private Long id;

    @Column(name="fecha_inicio") 
    private LocalDate fechaInicio;
    @Column(name="fecha_termino") 
    private LocalDate fechaTermino;

    private String sector;
    private String nombre;
    private String tema;

   @OneToMany(mappedBy = "activity",
              cascade = CascadeType.ALL,
              orphanRemoval = true,
              fetch = FetchType.LAZY)
   private List<Note> notas = new ArrayList<>();

    public Long getId() {
        return id;
    }

    public List<Note> getNotas() {
        return notas;
    }

    public LocalDate getFechaInicio() {
        return fechaInicio;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getTema() {
        return tema;
    }

    public void setId(Long id) { 
        this.id = id; 
    }
}
