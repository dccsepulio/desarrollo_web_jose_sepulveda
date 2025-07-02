package desarrollo_web.jose_sepulveda.tarea4.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface NoteRepository extends JpaRepository<Note,Long> {
   @Query("select avg(n.valor) from Note n where n.activity.id = :id")
   Double avgForActivity(@Param("id") Long id);
}
